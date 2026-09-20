import asyncio
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình Intents (Quyền cho Bot)
intents = commands.Intents.default()
intents.message_content = True  # Bắt buộc bật Message Content Intent trong Discord Developer Portal

# Khởi tạo Bot với tiền tố lệnh là !
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công dưới tên: {bot.user}")


@bot.command(name="start")
async def start_quiz(ctx):
    # Tạo ngẫu nhiên 2 số và 1 phép tính
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(["+", "-", "*"])

    # Tính toán đáp án đúng
    if operator == "+":
        correct_answer = num1 + num2
    elif operator == "-":
        correct_answer = num1 - num2
    else:
        correct_answer = num1 * num2

    # Gửi câu hỏi vào kênh Discord
    await ctx.send(f"❓ **Câu hỏi:** {num1} {operator} {num2} = ?\n*(Bạn có 15 giây để trả lời)*")

    # Hàm kiểm tra tin nhắn phản hồi
    def check(message):
        # Chỉ nhận tin nhắn từ cùng người dùng và cùng kênh chat
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Chờ người dùng nhập câu trả lời trong 15 giây
        msg = await bot.wait_for("message", timeout=15.0, check=check)

        # Kiểm tra xem câu trả lời có phải là số hay không
        if msg.content.strip().lstrip("-").isdigit():
            user_answer = int(msg.content.strip())
            if user_answer == correct_answer:
                await ctx.send(f"🎉 Chúc mừng {ctx.author.mention}! Bạn đã trả lời chính xác.")
            else:
                await ctx.send(
                    f"❌ Sai rồi {ctx.author.mention}! Đáp án đúng là: **{correct_answer}**."
                )
        else:
            await ctx.send(f"⚠️ {ctx.author.mention}, vui lòng chỉ nhập đáp án là một số!")

    except asyncio.TimeoutError:
        await ctx.send(
            f"⏰ Hết thời gian! {ctx.author.mention} đã không đưa ra câu trả lời. Đáp án đúng là: **{correct_answer}**."
        )


# Chạy bot bằng TOKEN lấy từ file .env hoặc biến môi trường
bot.run(os.getenv("TOKEN"))
          
