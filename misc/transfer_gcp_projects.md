# Transfer the GCP Project
[Reference](https://stackoverflow.com/questions/25697766/how-to-transfer-google-cloud-project-ownership)
Below are instructions to transfer GCP projects from one gmail account to another
* Goto IAM of the project on the old account
* Select `Grant Access`
* Specify the new gmail address and add it as Owner
* Goto the new gmail account and accept the invitation
* On the new account on GCP transfer the billing account of the project to this new account
* Optionally remove the old account as an Owner from the project

## Reset the gmail account on gcloud CLI on your local system
* Type `gcloud init` and reinitialize the configuration for the project and set the account to be used for operations as the new gmail account