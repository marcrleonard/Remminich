run this command:

```shell
sudo ansible-playbook deploy-app.yml -i inventory.ini --private-key="~/.ssh/id_rsa"
```

On the remote machine, you will likely need to modify your .ssh/config file. it should look something like this:

```
Host github.com
  StrictHostKeyChecking no
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_github
```

`StrictHostKeyChecking` is so the github clone doesn't fail if the machine hasn't ssh cloned from there before
`IdentityFile` is the key that is connected to github. This will need to be created on this remote machine and added to github.