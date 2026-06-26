import streamlit as st

from core.logger import Logger


class ErrorHandler:

    @staticmethod
    def execute(func, default=None):

        try:
            return func()

        except Exception as e:

            Logger.exception(str(e))

            st.error(
                "Something went wrong. The error has been logged."
            )

            return default
