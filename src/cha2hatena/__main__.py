from cha2hatena.main import main as async_main
import sys
import asyncio

def main():
    exit_code = asyncio.run(async_main())
    sys.exit(exit_code)

if __name__ == "__main__":
    main()