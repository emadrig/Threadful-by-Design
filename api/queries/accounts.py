from pydantic import BaseModel
from typing import Union, Optional, List
from queries.pool import pool



class Error(BaseModel):
  message:str

class AccountIn(BaseModel):
  username:str
  email:str
  password:str

class AccountOut(BaseModel):
  id:int
  username:str
  email:str
  password:str

class AccountRepository:
  def get_one(self, account_id:int) -> Optional[AccountOut]:
    try:
      with pool.connection() as conn:
        with conn.cursor() as db:
          result = db.execute(
            """
            SELECT id, username, email, password
            FROM accounts
            WHERE id = %s
            """,
            [account_id]
          )
          record = result.fetchone()
          if record is None:
            return None
          return self.record_to_account_out(record)
    except Exception as e:
      print(e)
      return {"message":"Could not find user account"}

  def delete(self, account_id)-> bool:
    try:
      with pool.connection() as conn:
        with conn.cursor() as db:
          db.execute(
            """
            DELETE FROM accounts
            WHERE id=%s
            """,
            [account_id]
          )
          return True
    except Exception as e:
      print(e)
      return False

  def update(self, account_id:int, account: AccountIn)-> Union[AccountOut, Error]:
    try:
      with pool.connection() as conn:
        with conn.cursor() as db:
          db.execute(
            """
            UPDATE accounts
            SET username=%s
              , email=%s
              , password=%s
            WHERE id=%s
            """,
            [
              account.username,
              account.email,
              account.password,
              account_id
            ]
          )
          return self.account_in_to_out(account_id, account)
    except Exception as e:
      print(e)
      return {"message":"Could not update account"}

  def get_all(self)-> Union[List[AccountOut], Error]:
    try:
      with pool.connection() as conn:
        with conn.cursor() as db:
          result = db.execute(
            """
            SELECT id, username, email, password
            FROM accounts
            ORDER BY username
            """
          )
          return [
            self.record_to_account_out(record)
            for record in result
            ]
    except Exception as e:
      print(e)
      return {"message":"Could not get all accounts"}

  def create(self, account:AccountIn)-> AccountOut:
    with pool.connection() as conn:
      with conn.cursor() as db:
        result = db.execute(
          """
          INSERT INTO accounts
            (username, email, password)
          VALUES
            (%s, %s, %s)
          RETURNING id;
          """,
          [
            account.username,
            account.email,
            account.password
          ]
        )
        id = result.fetchone()[0]
        return self.account_in_to_out(id, account)

  def account_in_to_out(self, id:int, account:AccountIn):
    old_data = account.dict()
    return AccountOut(id=id, **old_data)

  def record_to_account_out(self, record):
    return AccountOut(
      id=record[0],
      username=record[1],
      email=record[2],
      password=record[3],
    )
