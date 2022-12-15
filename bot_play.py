import os
import random
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import symbols as sm


def getToken():
    token = ''
    if os.path.isfile(sm.BOT_TOKEN_FILENAME):
        f = open(sm.BOT_TOKEN_FILENAME, "r")
        token = f.read()
        f.close()
    else:
        print("Пожалуйста, создайте в папке проекта файл 'token.txt' и поместите туда токен для работы телеграм бота  и запустите скрипт заново")
        sys.exit()
    return token


def isWin(arr, who):
    if (((arr[0] == who) and (arr[4] == who) and (arr[8] == who)) or
            ((arr[2] == who) and (arr[4] == who) and (arr[6] == who)) or
            ((arr[0] == who) and (arr[1] == who) and (arr[2] == who)) or
            ((arr[3] == who) and (arr[4] == who) and (arr[5] == who)) or
            ((arr[6] == who) and (arr[7] == who) and (arr[8] == who)) or
            ((arr[0] == who) and (arr[3] == who) and (arr[6] == who)) or
            ((arr[1] == who) and (arr[4] == who) and (arr[7] == who)) or
            ((arr[2] == who) and (arr[5] == who) and (arr[8] == who))):
        return True
    return False


def countUndefinedCells(cellArray):
    counter = 0
    for i in cellArray:
        if i == sm.SYMBOL_UNDEF:
            counter += 1
    return counter


def game(callBackData):
    message = sm.ANSW_YOUR_TURN
    alert = None

    buttonNumber = int(callBackData[0])
    if not buttonNumber == 9:
        charList = list(callBackData)
        charList.pop(0)
        if charList[buttonNumber] == sm.SYMBOL_UNDEF:
            charList[buttonNumber] = sm.SYMBOL_X 
            if isWin(charList, sm.SYMBOL_X):
                message = sm.ANSW_YOU_WIN
            else:
                if countUndefinedCells(charList) != 0:
                    isCycleContinue = True
                    while (isCycleContinue):
                        rand = random.randint(0, 8)
                        if charList[rand] == sm.SYMBOL_UNDEF:
                            charList[rand] = sm.SYMBOL_O
                            isCycleContinue = False
                            if isWin(charList, sm.SYMBOL_O):
                                message = sm.ANSW_BOT_WIN
        else:
            alert = sm.ALERT_CANNOT_MOVE_TO_THIS_CELL
        if countUndefinedCells(charList) == 0 and message == sm.ANSW_YOUR_TURN:
            message = sm.ANSW_DRAW
        callBackData = ''
        for c in charList:
            callBackData += c
    if message == sm.ANSW_YOU_WIN or message == sm.ANSW_BOT_WIN or message == sm.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += callBackData[j + i * 3] + ' | '
        callBackData = None

    return message, callBackData, alert


def getKeyboard(callBackData):
    keyboard = [[], [], []]
    if callBackData != None:
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(InlineKeyboardButton(callBackData[j + i * 3], callback_data=str(j + i * 3) + callBackData))

    return keyboard


def newGame(update, _):
    data = ''
    for i in range(0, 9):
        data += sm.SYMBOL_UNDEF

    update.message.reply_text(sm.ANSW_YOUR_TURN, reply_markup=InlineKeyboardMarkup(getKeyboard(data)))


def button(update, _):
    query = update.callback_query
    callbackData = query.data
    message, callbackData, alert = game(callbackData)
    if alert is None:
        query.answer()
        query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(getKeyboard(callbackData)))
    else:
        query.answer(text=alert, show_alert=True)


def help_command(update, _):
    update.message.reply_text(sm.ANSW_HELP)


