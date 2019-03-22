# Install the program
First get the json

```
name-your-contributors -o orbitdb --full --commits > orbit-db-contribs.json
```

We need to use full to get the createdAt and breakdown of each thing, but this won't send to csv because there's nesting

So to put it in a csv:

```
python3 script.py
```

For this to work properly this requires some changes to name-your-contributors that haven't been merged yet (primarily getting issueComments as well as just commitComments).