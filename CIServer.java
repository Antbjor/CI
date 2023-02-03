import java.net.*;
import java.io.*;


public class CIServer {
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;

    public void start(int port) {
        try{
            serverSocket = new ServerSocket(port);
            clientSocket = serverSocket.accept();
            System.out.println("Client connected");
            communication(clientSocket);
        }
        catch(Exception e){
            System.out.println("Server error: " + e);
        }
    }


    public void communication(Socket client) {
        try{
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            out = new PrintWriter(client.getOutputStream(), true);
            
            String s = "";
            while((s=in.readLine())!=null){
                System.out.println(s);
            }
        }
        catch(Exception e){
            System.out.println("Error handing in/out: " + e);
        }
    }

    public static void main(String[] args) {
        CIServer server=new CIServer();
        server.start(8030);
    }
}