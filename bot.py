import coinroll
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('target', type=int, default=0, help='profit target')
args = parser.parse_args()

MULTIPLIER = 2
LESSTHAN = int(0.99 / MULTIPLIER * 65536)

def color(n):
  return 32 if n >= 0 else 31

bot = coinroll.Coinroll(args.user, args.password)
r = bot.stats()
game = coinroll.gameinfo(LESSTHAN)
start = game['minbet']
amount = start

print 'every number is in satoshis except for lucky and less'
print 'balance  | amount   | lucky < less  | diff      | profit'

while r['balance'] > amount and r['profit'] < args.target:
  r = bot.bet(LESSTHAN, amount)
  print('%08d | %08d | \033[%dm%5d\033[m < %5d | \033[%dm%+09d\033[m | '
        '\033[%dm%+09d\033[m' % (r['balance'], r['amount'], color(r['diff']),
          r['lucky'], r['lessthan'], color(r['diff']), r['diff'],
          color(r['profit']), r['profit']))

  if r['win']:
    amount = start
  else:
    amount *= 2

    if amount > r['balance']:
      amount = start