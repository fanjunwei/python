import yaml
import subprocess
import StringIO
import os
def run_cmd(cmd):
    print cmd
    # p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    # code = p.wait()
    # if code:
    #     print ("{} \n{}\n{}".format(code,p.stderr.read(),p.stdout.read()))
    #     exit(code)
    code = os.system(cmd)
    if code!=0:
        exit(code)
def main():
    with open('repo.yml','r') as file:
        config = yaml.load(file)
    for i in config:
        if not os.path.exists(i.get("name")):
            cmd="git clone {} {}".format(i.get("repo"),i.get("name"))
            run_cmd(cmd=cmd)

    with open('merge.yml','r') as file:
        config = yaml.load(file)
    for i in config:
        cmd = "cd {};git fetch origin".format(i.get("name"))
        run_cmd(cmd=cmd)

        cmd="cd {};git checkout {} -f".format(i.get("name"),i.get("from"))
        run_cmd(cmd=cmd)
        cmd = "cd {};git pull".format(i.get("name"))
        run_cmd(cmd=cmd)

        cmd="cd {};git checkout {} -f".format(i.get("name"),i.get("to"))
        run_cmd(cmd=cmd)
        cmd = "cd {};git pull".format(i.get("name"))
        run_cmd(cmd=cmd)
        cmd = "cd {};git merge {}".format(i.get("name"),i.get("from"))
        run_cmd(cmd=cmd)
        cmd = "cd {};git push origin {}".format(i.get("name"),i.get("to"))
        run_cmd(cmd=cmd)


if __name__ == "__main__":
    main()