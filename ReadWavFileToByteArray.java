import java.io.InputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class ReadWavFileToByteArray {
    public static void main(String [] args) {
        try (FileInputStream inputStream = new FileInputStream(args[0])){
            byte[] bytes = new byte[4];
            byte[] bytes2 = new byte[2];
            int len;

            //Field 1
            len = inputStream.read(bytes, 0, bytes.length);
            System.out.println("First 4 bytes = " + new String(bytes));

            //Field 2 - chunkSize
            len = inputStream.read(bytes, 0, bytes.length);
            ByteBuffer buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes);
            buffer.rewind();
            int chunkSize = buffer.getInt();
            System.out.println("Next 4 bytes (chunkSize) = " + chunkSize);

            //Field 3 - format
            len = inputStream.read(bytes, 0, bytes.length);
            System.out.println("Next 4 bytes (format) = " + new String(bytes));

            //Field 4 - SubChunk1Id
            len = inputStream.read(bytes, 0, bytes.length);
            System.out.println("Next 4 bytes (subChunk1Id) = " + new String(bytes));

            //Field 5 - SubChunk1Size
            len = inputStream.read(bytes, 0, 4);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes);
            buffer.rewind();
            int subChunk1Size = buffer.getInt();
            System.out.println("Next 4 bytes (subChunk1Size) = " + subChunk1Size);

            //Field 6 - AudioFormat
            len = inputStream.read(bytes2, 0, 2);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes2);
            buffer.rewind();
            Short audioFormat = buffer.getShort();
            System.out.println("Next 2 bytes (audioFormat) = " + audioFormat);

            //Field 7 - NumberOfChannels
            len = inputStream.read(bytes2, 0, 2);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes2);
            buffer.rewind();
            Short numChannels = buffer.getShort();
            System.out.println("Next 2 bytes (numChannels) = " + numChannels);

            //Field 8 - SampleRate
            len = inputStream.read(bytes, 0, 4);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes);
            buffer.rewind();
            int sampleRate = buffer.getInt();
            System.out.println("Next 4 bytes (sampleRate) = " + sampleRate);

            //Field 9 - ByteRate
            len = inputStream.read(bytes, 0, 4);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes);
            buffer.rewind();
            int byteRate = buffer.getInt();
            System.out.println("Next 4 bytes (byteRate) = " + byteRate);

            //Field 10 - BlockAlign
            len = inputStream.read(bytes2, 0, 2);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes2);
            buffer.rewind();
            Short blockAlign = buffer.getShort();
            System.out.println("Next 2 bytes (blockAlign) = " + blockAlign);

            //Field 11 - BitsPerSample
            len = inputStream.read(bytes2, 0, 2);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes2);
            buffer.rewind();
            Short bitsPerSample = buffer.getShort();
            System.out.println("Next 2 bytes (bitsPerSample) = " + bitsPerSample);

            //Field 12 - SubChunk2Id
            len = inputStream.read(bytes, 0, bytes.length);
            System.out.println("Next 4 bytes (subChunk2Id) = " + new String(bytes));

            //Field 13 - SubChunk2Size
            len = inputStream.read(bytes, 0, 4);
            buffer = ByteBuffer.allocate(len);
            buffer.order(ByteOrder.LITTLE_ENDIAN); 
            buffer.put(bytes);
            buffer.rewind();
            int subChunk2Size = buffer.getInt();
            System.out.println("Next 4 bytes (subChunk2Size) = " + subChunk2Size);

            System.out.println(subChunk2Size % numChannels*(bitsPerSample)/8);

            byte[] data = new byte[subChunk2Size];
            len = inputStream.read(data,0,data.length);
            System.out.println("data read len = " + len);
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }
}
