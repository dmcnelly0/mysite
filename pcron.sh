cd /home/ec2-user/mysite
echo "Did run." > didrun.out
python3 manage.py shell <<EOF
print("Starting")
from survey.cron import run_
print("Import")
run_()
exit()
EOF
