rm *.gz
tar czf "bkp-$FTP_FILE-$(date +%Y%m%d_%H%M%S).tar.gz" minecraft
curl --user $FTP_USERNAME:$FTP_PASSWORD -T bkp* $FTP_SERVER/

mv bkp* bkp-$FTP_FILE-latest.tar.gz
curl --user $FTP_USERNAME:$FTP_PASSWORD -T bkp* $FTP_SERVER/