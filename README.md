Makes it easier to play tlog recordings in elasticsearch, by finding all relevant sessions and presenting them in a menu

Requires `dialog` installed, python3.6 or newer, and the tlog-play binary in your $PATH

# Usage
```
usage: player.py [-h] --es-host ES_HOST --es-index ES_INDEX [--query QUERY]

List tlog sessions that can be played back

optional arguments:
  -h, --help           show this help message and exit
  --es-host ES_HOST    Elasticsearch server hostname[:port]
  --es-index ES_INDEX  Index tlog stores recordings in
  --query QUERY        Elasticsearch query string, see
                       https://github.com/Scribery/tlog#playing-back-from-elasticsearch for example query string
```
