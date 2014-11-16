We should write an observer setup script that involves:
# sudo mkdir /usr/local/gallery
# chown pi:pi /usr/local/gallery
# mkdir /usr/local/gallery/jar
# mkdir /usr/local/gallery/src
# cd /usr/local/gallery/jar
# wget http://repo1.maven.org/maven2/com/google/zxing/core/3.1.0/core-3.1.0.jar
# wget http://repo1.maven.org/maven2/com/google/zxing/javase/3.1.0/javase-3.1.0.jar
# wget http://repo1.maven.org/maven2/com/google/zxing/zxingorg/3.1.0/zxingorg-3.1.0.war
# export CLASSPATH=$CLASSPATH:/usr/local/gallery/jar
# cd /usr/local/gallery/src
# wget http://javapapers.com/wp-content/uploads/2013/10/QRCode.zip
# unzip QRCode.zip
# javac -cp /usr/local/gallery/jar/core-3.1.0.jar:/usr/local/gallery/jar/javase-3.1.0.jar:/usr/local/gallery/jar/zxingorg-3.1.0.war QRCode.java
# java QRCode
