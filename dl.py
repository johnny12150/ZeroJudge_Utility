from urllib.request import urlretrieve
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("number", help="question number")
args = parser.parse_args()

def main(problem_num):
    dl_str = "https://uva.onlinejudge.org/external/"+ str(int(problem_num/100)) +"/"+ str(problem_num) +".pdf"
    urlretrieve(dl_str, "uva_" + str(problem_num) + ".pdf")
    
    print(dl_str)


#files = [100, 488, 913, 11150, 11877, 10035, 10055, 10071, 10550, 10673, 10696, 10783, 10812, 10929, 11172, 11332, 11479, 11689, 11743, 11764, 12019, 12149, 12459, 12468, 13187]
question_list = args.number.split()

for i in question_list:
    main(int(i))
    file_name = "uva_"+i+".pdf"
    subprocess.check_call(["sudo", "mv", file_name, "/var/lib/tomcat8/webapps/ROOT/PDF/"])
