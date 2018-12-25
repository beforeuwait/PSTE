# coding=utf-8

__author__ = 'wangjiawei'
__date__ = '2018-11-27'

"""
    对HTTP模块进行重构
    并不添加新功能
    ================================
    2018-11-27：当前能用的只有
    get/post 请求
"""

__all__ = ['RequestAPI']

from HTTP.HttpApi import HttpApi as RequestAPI
