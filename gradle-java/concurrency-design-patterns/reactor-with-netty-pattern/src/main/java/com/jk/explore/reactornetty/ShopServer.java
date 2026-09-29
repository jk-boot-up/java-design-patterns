package com.jk.explore.reactornetty;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.MultiThreadIoEventLoopGroup;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.channel.nio.NioIoHandler;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.LineBasedFrameDecoder;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;
import io.netty.util.concurrent.DefaultEventExecutorGroup;
import io.netty.util.concurrent.EventExecutorGroup;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * The shop's stock server on Netty. A boss event loop accepts connections; worker event loops, each a
 * reactor on one thread, wait on many connections at once and run the handlers.
 */
public final class ShopServer implements AutoCloseable {

    static final Map<String, Integer> STOCK = Map.of("KETTLE-1", 4, "MUG-1", 25);
    static final Map<String, Integer> PRICE = Map.of("KETTLE-1", 3000, "MUG-1", 800);

    private final EventLoopGroup boss = new MultiThreadIoEventLoopGroup(1, NioIoHandler.newFactory());
    private final EventLoopGroup workers;
    private final EventExecutorGroup slowWork;
    private final Set<String> handlerThreads = ConcurrentHashMap.newKeySet();
    private final Map<Channel, String> threadOfConnection = new ConcurrentHashMap<>();
    private final Channel server;

    /** {@code offloadSlow}: run the handler on a separate group of threads, away from the event loop. */
    public ShopServer(int workerThreads, boolean offloadSlow) throws InterruptedException {
        workers = new MultiThreadIoEventLoopGroup(workerThreads, NioIoHandler.newFactory());
        slowWork = offloadSlow ? new DefaultEventExecutorGroup(4) : null;
        server = new ServerBootstrap()
                .group(boss, workers)
                .channel(NioServerSocketChannel.class)
                .childHandler(new ChannelInitializer<SocketChannel>() {
                    @Override
                    protected void initChannel(SocketChannel ch) {
                        ch.pipeline().addLast(new LineBasedFrameDecoder(256));   // bytes -> whole lines
                        ch.pipeline().addLast(new StringDecoder(StandardCharsets.UTF_8));
                        ch.pipeline().addLast(new StringEncoder(StandardCharsets.UTF_8));
                        if (slowWork != null) {
                            ch.pipeline().addLast(slowWork, new QuestionHandler());
                        } else {
                            ch.pipeline().addLast(new QuestionHandler());
                        }
                    }
                })
                .bind("127.0.0.1", 0).sync().channel();
    }

    public int port() {
        return ((java.net.InetSocketAddress) server.localAddress()).getPort();
    }

    public int handlerThreads() {
        return handlerThreads.size();
    }

    public int eventLoopsServingConnections() {
        return (int) threadOfConnection.values().stream().distinct().count();
    }

    public void forgetThreads() {
        handlerThreads.clear();
        threadOfConnection.clear();
    }

    /** One question per line: "stock SKU", "price SKU", or "report" (slow). */
    final class QuestionHandler extends SimpleChannelInboundHandler<String> {

        @Override
        public void channelActive(ChannelHandlerContext ctx) {
            threadOfConnection.put(ctx.channel(), Thread.currentThread().getName());
        }

        @Override
        protected void channelRead0(ChannelHandlerContext ctx, String line) throws Exception {
            handlerThreads.add(Thread.currentThread().getName());
            String[] q = line.trim().split(" ");
            String answer = switch (q[0]) {
                case "stock" -> String.valueOf(STOCK.getOrDefault(q[1], 0));
                case "price" -> String.valueOf(PRICE.getOrDefault(q[1], 0));
                case "report" -> {
                    Thread.sleep(300);   // a slow report, blocking whichever thread runs it
                    yield "report ready";
                }
                default -> "unknown";
            };
            ctx.writeAndFlush(answer + "\n");
        }
    }

    @Override
    public void close() {
        server.close().syncUninterruptibly();
        boss.shutdownGracefully().syncUninterruptibly();
        workers.shutdownGracefully().syncUninterruptibly();
        if (slowWork != null) {
            slowWork.shutdownGracefully().syncUninterruptibly();
        }
    }
}
