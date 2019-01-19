package TestConnections;

import java.net.*;
import java.io.*;

class TCPClient {
  public static void main(String argv[]) throws Exception {
    // Init empty vars
    String sentence;
    String modifiedSentence;
    // Connect to ip
    Socket clientSocket = new Socket("192.168.1.7", 5050); // 192.168.1.7
    System.out.println("Succsessfully opened port");
    // Init ins and outs
    PrintWriter outToServer = new PrintWriter(clientSocket.getOutputStream(), true);
    BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    // Scentence to be sent
    sentence = "@ping";
    // Starting ping time
    long start_time = System.nanoTime();
    // Send data to server
    outToServer.println(sentence);
    // Read data from server
    modifiedSentence = inFromServer.readLine();
    // Ending ping time
    long end_time = System.nanoTime();
    // Calculate ping
    double difference = (end_time - start_time) / 1e6;
    // Print data and ping
    System.out.println(modifiedSentence);
    System.out.println("\n\n\nping: " + difference + " ms");
    // Close socket connection
    clientSocket.close();
  }
 }