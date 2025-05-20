from .db import AsyncDB
import asyncio

async def user_exists(telegram_id):
    result = await AsyncDB().execute_query("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
    return bool(result)

async def add_user(telegram_id, first_name, last_name, username):
    await AsyncDB().execute_query("INSERT INTO users(telegram_id, first_name, last_name, username) VALUES($1,$2,$3,$4)", telegram_id, first_name, last_name, username)

async def reduce_user_limit(telegram_id):
    await AsyncDB().execute_query("UPDATE users SET limit_rq=limit_rq-1 WHERE telegram_id=$1", telegram_id)

async def update_limit():
    await AsyncDB().execute_query("UPDATE users SET limit_rq = 2")

#async def reduce_user_limit_pay(telegram_id):
 #   await AsyncDB().execute_query("UPDATE users SET limit_pay=limit_pay-1 WHERE telegram_id=$1", telegram_id)

#async def update_limit_pay():
 #   await AsyncDB().execute_query("UPDATE users SET limit_pay = 25")

async def update_user_active(telegram_id, status):
    await AsyncDB().execute_query("UPDATE users SET is_active=$1 WHERE telegram_id=$2", status, telegram_id)

async def get_user_limit(telegram_id):
    result = await AsyncDB().execute_query("SELECT limit_rq FROM users WHERE telegram_id=$1", telegram_id)
    return result[0]['limit_rq'] if result else None

async def update_label_period(label, period, telegram_id):
    return await AsyncDB().execute_query("UPDATE users SET label=$1, period=$2 WHERE telegram_id=$3",label, period, telegram_id)

async def get_payment_status(telegram_id):
    return await AsyncDB().execute_query("SELECT is_subscribed, label, period FROM users WHERE telegram_id=$1",telegram_id)

async def get_user_id(telegram_id):
    return await AsyncDB().execute_query("SELECT telegram_id from users where telegram_id=$1",telegram_id)

async def update_payment_status(telegram_id):
    return await AsyncDB().execute_query("UPDATE users SET is_subscribed=True WHERE telegram_id=$1",telegram_id)

async def user_subscribed(telegram_id):
    result = await AsyncDB().execute_query("SELECT id FROM users WHERE telegram_id = $1 AND is_subscribed = True", telegram_id)
    return bool(result)
print ('3')    
    
async def get_user_subscr_exp(telegram_id):
    result = await AsyncDB().execute_query("SELECT subscr_exp FROM users WHERE telegram_id = $1", telegram_id)
    return result[0]['subscr_exp'] if result else None
print ('4')

async def set_user_subscribed(exp_date,telegram_id):
    return await AsyncDB().execute_query("UPDATE users SET is_subscribed=True, subscr_exp=$1 WHERE telegram_id=$2", exp_date, telegram_id)
print ('5')    

async def get_expired_subs(current_time):
    result = await AsyncDB().execute_query("SELECT telegram_id FROM users WHERE subscr_exp < $1 AND is_subscribed = True", current_time)
    tg_id_list = list()
    for record in result:
        if record['telegram_id'] not in tg_id_list:
            tg_id_list.append(record['telegram_id'])
    return tg_id_list

async def set_user_unsubdcribed(telegram_id):
    return await AsyncDB().execute_query("UPDATE users set is_subscribed = False where telegram_id=$1",telegram_id) 
print ('6')

     

async def main():
    import datetime
    await set_user_subscribed(datetime.datetime.now() + datetime.timedelta(hours = 1),2089545494)

if __name__ == "__main__":
    asyncio.run(main())
