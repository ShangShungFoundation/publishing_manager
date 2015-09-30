set -x
#USAGE: ./mp3.sh "Artur Skura" arturs@people.pl "Guru_Yoga_of_the_White_A"
#USER_STRING="Artur Skura"
#PRODNAME="Guru_Yoga_of_the_White_A"
USER_STRING=$1
#USER_STRING2=${USER_STRING// /%20}
USER_MAIL=$2
PRODNAME=$3

OUTFILE=$PRODNAME".zip"
rm $OUTFILE
rm -r $PRODNAME
mkdir $PRODNAME
cp 1/$PRODNAME/* $PRODNAME
cd $PRODNAME
id3tag -c "\"Licensed to: $USER_STRING"\" *.mp3
id3tag -a "Choegyal Namkhai Norbu" *.mp3
uuid -F BIN > uuid.bin
UUID=`/usr/bin/decu.py uuid.bin`
for i in *.mp3; do cat "$i" uuid.bin > test.mp3; mv -f test.mp3 "$i"; done
echo -e "$USER_STRING \t $USER_MAIL \t $PRODNAME \t $UUID" >> ../uuid.txt
rm -f uuid.bin
cd ..
zip -r $PRODNAME $PRODNAME

ls -al $OUTFILE

##############

RAND_DIR=`pwgen 40 1`
mkdir /var/www/mmllib/$RAND_DIR

# the final file copied to the random directory; current user must be in www-data
mv $OUTFILE /var/www/mmllib/$RAND_DIR/$OUTFILE

# mail generated
echo "Dear $USER_STRING," > mailfile.txt
echo "" >> mailfile.txt
echo "We are pleased to inform you that the MP3 archive you ordered is ready " >> mailfile.txt
echo "for download. This MP3 set is exclusively intended for those who have " >> mailfile.txt
echo "already received the transmission of the practices it contains. " >> mailfile.txt
echo "The archive is licensed to you for your personal use only and " >> mailfile.txt
echo "cannot be reproduced in any form. We strongly urge you to treat " >> mailfile.txt 
echo "the files with respect and store them in a safe location." >> mailfile.txt
echo "" >> mailfile.txt

echo "Download link: " >> mailfile.txt
echo "http://p.shangshungpublications.org/mmllib/$RAND_DIR/$OUTFILE" >> mailfile.txt
echo "" >> mailfile.txt
echo "Right-click on the download link and choose \"Save File As\" to " >> mailfile.txt 
echo "save it to your computer. " >> mailfile.txt
echo "Please download the file as soon as you can as the download " >> mailfile.txt 
echo "link will expire in 3 days." >> mailfile.txt

echo "" >> mailfile.txt
echo "We wish you a good practice!"  >> mailfile.txt
echo "Shang Shung Publications Team"  >> mailfile.txt
echo "http://www.shangshungstore.org"  >> mailfile.txt

# mail sent
# (when reinstalling, check mail domain in exim)
# note that BSD mail supports the -aHEADER option,
bsd-mailx -aFrom:orders@shangshungpublications.org -s "Download link for $USER_STRING" -c orders@shangshungpublications.org $USER_MAIL <mailfile.txt
#bsd-mailx -aFrom:orders@shangshungpublications.org -s "Download link for $USER_STRING"  $USER_MAIL <mailfile.txt
rm mailfile.txt