rm bkp*
rm -r minecraft
curl --user $FTP_USERNAME:$FTP_PASSWORD $FTP_SERVER/bkp-$FTP_FILE-latest.tar.gz -o bkp.tar.gz
tar -xzf bkp*
rm bkp*
