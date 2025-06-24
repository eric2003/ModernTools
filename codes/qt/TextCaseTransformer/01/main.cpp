#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QTextEdit>
#include <QLabel>
#include <QString>

class CaseConverterWindow : public QMainWindow {
    Q_OBJECT

public:
    CaseConverterWindow(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("String Case Converter");
        setFixedSize(400, 300);

        // 创建主窗口部件和布局
        QWidget *centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);
        QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

        // 输入标签
        QLabel *inputLabel = new QLabel("Enter Text:", centralWidget);
        inputLabel->setStyleSheet("font-size: 12pt; font-family: Arial;");
        mainLayout->addWidget(inputLabel);

        // 输入文本框
        inputField = new QTextEdit(centralWidget);
        inputField->setFixedHeight(80);
        inputField->setStyleSheet("font-size: 10pt; font-family: Arial;");
        mainLayout->addWidget(inputField);

        // 按钮布局
        QHBoxLayout *buttonLayout = new QHBoxLayout();
        mainLayout->addLayout(buttonLayout);

        // 大写按钮
        QPushButton *upperButton = new QPushButton("To Upper Case", centralWidget);
        upperButton->setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;");
        connect(upperButton, &QPushButton::clicked, this, &CaseConverterWindow::toUpperCase);
        buttonLayout->addWidget(upperButton);

        // 小写按钮
        QPushButton *lowerButton = new QPushButton("To Lower Case", centralWidget);
        lowerButton->setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;");
        connect(lowerButton, &QPushButton::clicked, this, &CaseConverterWindow::toLowerCase);
        buttonLayout->addWidget(lowerButton);

        // 结果文本框（可复制）
        resultField = new QTextEdit(centralWidget);
        resultField->setFixedHeight(80);
        resultField->setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;");
        resultField->setText("Result will appear here");
        resultField->setReadOnly(false); // 允许复制
        mainLayout->addWidget(resultField);

        // 添加拉伸以保持布局整洁
        mainLayout->addStretch();

        // 设置窗口背景
        setStyleSheet("background-color: #f0f0f0;");
    }

private slots:
    void toUpperCase() {
        QString inputText = inputField->toPlainText().trimmed();
        resultField->setText(inputText.toUpper());
    }

    void toLowerCase() {
        QString inputText = inputField->toPlainText().trimmed();
        resultField->setText(inputText.toLower());
    }

private:
    QTextEdit *inputField;
    QTextEdit *resultField;
};

#include "main.moc"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    CaseConverterWindow window;
    window.show();
    return app.exec();
}