# Ingredient Calculator

Ingredient conversion calculator converts ingredient measurements from mass to volume (or vice versa). 
Often recipes will give instructions in terms of cups or tablespoons,
but when scaling up recipes it's often more desirable use weight to determine ingredient amounts.

## Deployment

The ingredient conversion function is implemented in Python and hosted on 
[Digital Ocean's Function platform](https://cloud.digitalocean.com/functions/). 

The function is invoked using the Javascript `fetch` api. 

To deploy this function, ensure you have `doctl` installed and connected to your Digital Ocean account.
See [Digital Ocean Function Quickstart](https://docs.digitalocean.com/products/functions/quickstart/) for details.
You can then run:

```bash
$ make deploy
```
## Resources

- [Digital Ocean Function Quickstart](https://docs.digitalocean.com/products/functions/quickstart/)
- [Javascript `fetch` API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
