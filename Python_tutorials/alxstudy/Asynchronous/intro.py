#!usr/bin/env python3
import asyncio


async def task1():
  print("Wake up started")
  await asyncio.sleep(1)
  print("Wake up completed")


async def task2():
  print("Take a shower started")
  await asyncio.sleep(2)
  print("Take a shower completed")


async def task3():
  print("Have Breakfast started")
  await asyncio.sleep(4)
  print("Have Breakfast completed")


async def main():
  await asyncio.gather(task1(), task2(), task3())

asyncio.run(main())
