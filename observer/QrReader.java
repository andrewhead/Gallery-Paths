import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.TimeZone;
import javax.imageio.ImageIO;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.EncodeHintType;
import com.google.zxing.MultiFormatReader;
import com.google.zxing.NotFoundException;
import com.google.zxing.Result;
import com.google.zxing.ResultPoint;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;


/**
 *  Reads and displays data and coordinates from QR codes in JPEG files.
 *  Code based on: http://javapapers.com/core-java/java-qr-code/.
 */
public class QrReader {

	public static void main(String[] args) throws IOException, NotFoundException {
        /**
         *  @param args list of filenames to process
         */
		Map<EncodeHintType, ErrorCorrectionLevel> hintMap = new HashMap<EncodeHintType, ErrorCorrectionLevel>();
		hintMap.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.L);

        for (int i = 0; i < args.length; i++) {
            /* Compute the value of the QR code */
            String filePath = args[0];
            Result qrCode = readQRCode(filePath, "UTF-8", hintMap);

            /* Start by printing out date, which should be encoded in the file's basename */
            String basename = new File(filePath).getName().split("\\.")[0];
            System.out.print(basename + ",");

            /* Print out QRCode detection information */
            ResultPoint[] qrPoints = qrCode.getResultPoints();
            System.out.print(qrCode.getText() + ",");
            for (int j = 0; j < qrPoints.length; j++) {
                System.out.print(qrPoints[j].getX() + "," + qrPoints[j].getY() + ",");
            }
            System.out.println();
        }
	}

	public static Result readQRCode(String filename, String charset, Map hintMap)
        /**
         *  Read QR code from image file.
         */
        throws FileNotFoundException, IOException, NotFoundException {
		BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(
				new BufferedImageLuminanceSource(ImageIO.read(new FileInputStream(filename)))));
		Result qrCode = new MultiFormatReader().decode(binaryBitmap, hintMap);
        return qrCode;
	}
}
