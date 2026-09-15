from db import init_db, save_message

init_db()
save_message("a", "user", "第一条")
save_message("b", "assistant", "第二条")
save_message("b", "user", "另外一条")
print("写完了。")