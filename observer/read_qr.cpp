#include <iostream>
#include <fstream>
#include <zbar.h>
#include <time.h>
#include <sys/stat.h>
#define STR(s) #s

using namespace std;
using namespace zbar;

char* readFileBytes(const char *name)
{
    ifstream fl(name);
    fl.seekg(0, ios::end);
    size_t len = fl.tellg();
    char *ret = new char[len];
    fl.seekg(0, ios::beg);
    fl.read(ret, len);
    fl.close();
    return ret;
}

char* getFileTimestamp(const char *name) {
	struct stat fileStat;
    stat(name, &fileStat);
    struct tm* accessTime = gmtime(&fileStat.st_mtime);
    char* timeStr = new char[21];
    strftime(timeStr, 21, "%Y-%m-%dT%H:%M:%SZ", accessTime);
    return timeStr;
}

void printTime(const char *msg) 
{
    time_t currTime = time(NULL);
    printf("Point: %s. Time: %s\n", msg, asctime(localtime(&currTime)));
}

int main (int argc, char **argv)
{
    if(argc < 2) return(1);

    // create a reader
    ImageScanner scanner;

    // configure the reader
    scanner.set_config(ZBAR_NONE, ZBAR_CFG_ENABLE, 1);

    // obtain image data
    const void *raw = readFileBytes(argv[1]);

    // wrap image data
	int w = atoi(argv[2]);
	int h = atoi(argv[3]);
    Image image(w, h, "Y800", raw, w * h);

    // scan the image for barcodes
    int n = scanner.scan(image);

    // extract results
    for(Image::SymbolIterator symbol = image.symbol_begin();
        symbol != image.symbol_end();
        ++symbol) {
        // do something useful with results
        cout << getFileTimestamp(argv[1]) << "," << symbol->get_data() << ",";
        for(int i = 0; i < symbol->get_location_size(); i++) 
        {
            printf("%d,%d,", symbol->get_location_x(i), symbol->get_location_y(i));
        }
        cout << endl;
    }

    /* Clean up */
    image.set_data(NULL, 0);

    return(0);
}
