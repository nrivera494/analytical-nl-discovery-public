"""Sequential runner, gpt-d/gpt-6-astra/gpt; never parallelizes propagation."""
from independent import *
for cfg in sys.argv[1:]:
    while True:
        try: memory_ok();break
        except SystemExit:
            print('Waiting 30 seconds for shared-machine memory',flush=True);time.sleep(30)
    execute(cfg)
