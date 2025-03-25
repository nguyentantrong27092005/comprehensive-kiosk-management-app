import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget,
                             QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal
from google import genai
from google.genai import types

class AnalysisWorker(QThread):
    output_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    analysis_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = genai.Client()

    def run(self):
        document1 = types.Part.from_uri(
            file_uri="gs://kioskappstorage/mysql_aggregated_data/best_seller.txt",
            mime_type="text/plain",
        )
        document2 = types.Part.from_uri(
            file_uri="gs://kioskappstorage/mysql_aggregated_data/evoucher.txt",
            mime_type="text/plain",
        )
        document3 = types.Part.from_uri(
            file_uri="gs://kioskappstorage/mysql_aggregated_data/mon_duoc_tang.txt",
            mime_type="text/plain",
        )
        document4 = types.Part.from_uri(
            file_uri="gs://kioskappstorage/mysql_aggregated_data/tong_doanh_thu_monthly.txt",
            mime_type="text/plain",
        )
        document5 = types.Part.from_uri(
            file_uri="gs://kioskappstorage/mysql_aggregated_data/tong_doanh_thu_weekly.txt",
            mime_type="text/plain",
        )

        si_text1 = """You are a data analyst specializing in restaurant sales. Your goal is to provide actionable insights in a professional and concise manner. You will be given the following files: sales by dishes, promotion data, revenue, discount and profit group by week or month. These files are in txt format with the delimiter is comma.
            You should combine all these data to analyze the following ideas:
            - Trends of revenue, profit, best seller dishes. Also predict how these trend would change in the future.
            - Factors that could affect these trends (maybe because of the promotion programs listing in the given promotion data).
            Then you should give the owner of the restaurant how to enhance their business. And please don't list out the given data files, just focus on the analysis."""

        model = "gemini-2.0-flash-001"
        contents = [
            types.Content(
                role="user",
                parts=[
                    document1,
                    document2,
                    document3,
                    document4,
                    document5,
                    types.Part.from_text(
                        text="""Please rely on the given instruction to analyze the given data in Vietnamese."""
                    )
                ]
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=[types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )],
            system_instruction=[types.Part.from_text(text=si_text1)],
        )

        for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            try:
                self.output_received.emit(chunk.text)
            except:
                print("Waiting")

        self.analysis_finished.emit()

class AIPromptViewEx(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Analysis Integration")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.run_button = QPushButton("Chạy lại Phân tích")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #BD1906;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: gray;
                color: lightgray;
            }
        """)
        self.run_button.setMinimumHeight(40)
        self.layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.start_analysis)

        self.output_area = QTextBrowser()
        self.output_area.setOpenExternalLinks(True)
        self.layout.addWidget(self.output_area)
        self.current_raw_text = ""

        self.worker_thread = None
        # self.start_analysis()

    def start_analysis(self):
        print("Start analyzing...")
        self.output_area.clear()
        self.output_area.setMarkdown("**Đang đợi trợ thủ AI đắc lực của bạn suy nghĩ...**\n")
        self.run_button.setEnabled(False)

        self.worker_thread = AnalysisWorker(self)
        self.worker_thread.output_received.connect(self.update_output)
        self.worker_thread.error_occurred.connect(self.handle_error)
        self.worker_thread.analysis_finished.connect(self.analysis_complete)
        self.worker_thread.start()

    def update_output(self, text):
        """Append new text in markdown format."""
        self.current_raw_text += text
        self.output_area.setMarkdown(self.current_raw_text)

    def handle_error(self, message):
        QMessageBox.critical(self, "Analysis Error", message)
        self.run_button.setEnabled(True)

    def analysis_complete(self):
        self.output_area.setMarkdown(self.output_area.toMarkdown() + "\n**Đã phân tích xong.**")
        self.run_button.setEnabled(True)

