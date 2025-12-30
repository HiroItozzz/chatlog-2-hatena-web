import asyncio
import sys

from cha2hatena.main import main as async_main


def main():
    exit_code = asyncio.run(async_main())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
