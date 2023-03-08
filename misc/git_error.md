### Link the remote VM to sf_eviction remote repo
* `git clone https://github.com/sanyassyed/sf_eviction.git` on the remote VM
* `git add .` -> after making changes
* `git config --global user.email "sanya.shireen@gmail.com"`
* `git config --global user.name "sanya googlevm"`
* `git commit -m "CICD: Updated gitignore from VM"`
* `git push -u origin master` -> after this enter the user name and the personal access token for password

### Avoid having to enter the password and user name each time on the VM
* Create a SSH key pair as follows
```bash
   ssh-keygen -t rsa
   /home/sanyashireen/.ssh/vm_rsa
```
* Add the public key to you github account
* create a `config` file
    - `nano config` and write the below to file
    - Host sanyassyed.github.com
           HostName github.com
           PreferredAuthentications publickey
           IdentityFile /home/sanyashireen/.ssh/vm_rsa
* Check the SSH connection with repo from VM using
```bash
$ ssh -T git@github.com
$ ssh -vT git@github.com
``` 
* ERROR: public key denied and cannot resolve host
    - Soln: Earlier we cloned the repo using http so the remote origin is set using https:
    - check this using 
    ```bash
       git remote -v
       origin  https://github.com/sanyassyed/sf_eviction.git (fetch)
       origin  https://github.com/sanyassyed/sf_eviction.git (push)
    ```
    - change the origin from https to ssh as follows
    ```bash
       git remote set-url origin git@github.com:sanyassyed/sf_eviction.git
       git remote -v
       origin  git@github.com:sanyassyed/sf_eviction.git (fetch)
       origin  git@github.com:sanyassyed/sf_eviction.git (push)
    ```
* Still the Permission denied error (public key) [Soln Source](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey)
```bash
    # start ssh agent 
    eval `ssh-agent -s`	
    ssh-add -l -E sha256
    > The agent has no identities.
    # guide the ssh agent where the keys are stored
    ssh-add /home/sanyashireen/.ssh/vm_rsa
    > Identity added: /home/sanyashireen/.ssh/vm_rsa (sanyashireen@de-zoomcamp)
```