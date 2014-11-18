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
		String filePath = args[0];
		Map<EncodeHintType, ErrorCorrectionLevel> hintMap = new HashMap<EncodeHintType, ErrorCorrectionLevel>();
		hintMap.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.L);
        Result qrCode = readQRCode(filePath, "UTF-8", hintMap);

        /* Start by printing out date */
        TimeZone timezone = TimeZone.getTimeZone("UTC");
        DateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        format.setTimeZone(timezone);
        System.out.print(format.format(new Date()) + ",");

        /* Print out QRCode detection information */
		ResultPoint[] qrPoints = qrCode.getResultPoints();
		System.out.print(qrCode.getText() + ",");
		for (int i = 0; i < qrPoints.length; i++) {
		    System.out.print(qrPoints[i].getX() + "," + qrPoints[i].getY() + ",");
		}
        System.out.println();
	}

	public static Result readQRCode(String filename, String charset, Map hintMap)
        /* Read QR code from image file */
        throws FileNotFoundException, IOException, NotFoundException {
		BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(
				new BufferedImageLuminanceSource(ImageIO.read(new FileInputStream(filename)))));
		Result qrCode = new MultiFormatReader().decode(binaryBitmap, hintMap);
        return qrCode;
	}
}
