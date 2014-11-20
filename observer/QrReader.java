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
import com.google.zxing.multi.qrcode.QRCodeMultiReader;
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
            Result[] qrCodes = null;
            try {
                qrCodes = readQRCodes(filePath, "UTF-8", hintMap);
            } catch (NotFoundException nfe) {
                continue;
            }

            if (qrCodes != null) {
                for (int j = 0; j < qrCodes.length; j++) {

                    /* Start by printing out date, which should be encoded in the file's basename */
                    Result qrCode = qrCodes[j];
                    String basename = new File(filePath).getName().split("\\.")[0];
                    System.out.print(basename + ",");

                    /* Print out QRCode detection information */
                    ResultPoint[] qrPoints = qrCode.getResultPoints();
                    System.out.print(qrCode.getText() + ",");
                    for (int k = 0; k < qrPoints.length; k++) {
                        System.out.print(qrPoints[k].getX() + "," + qrPoints[k].getY() + ",");
                    }
                    System.out.println();
                }
            }
        }
	}

	public static Result[] readQRCodes(String filename, String charset, Map hintMap)
        /**
         *  Read QR codes from image file.
         */
        throws FileNotFoundException, IOException, NotFoundException {
		BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(
				new BufferedImageLuminanceSource(ImageIO.read(new FileInputStream(filename)))));
		Result[] qrCodes = new QRCodeMultiReader().decodeMultiple(binaryBitmap, hintMap);
        return qrCodes;
	}
}
