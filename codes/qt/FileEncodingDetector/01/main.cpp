#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QPushButton>
#include <QTextEdit>
#include <QFileDialog>
#include <QLabel>
#include <QString>
#include <QFile>
#include <QTextStream>
#include <QStringConverter>

class EncodingDetectorWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit EncodingDetectorWindow(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("文件编码检测器");
        setFixedSize(500, 350);

        // 创建主窗口部件和布局
        QWidget *centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);
        QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

        // 标题标签
        QLabel *titleLabel = new QLabel("文件编码检测器", centralWidget);
        titleLabel->setStyleSheet("font-size: 14pt; font-family: Arial; font-weight: bold;");
        titleLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(titleLabel);

        // 选择文件按钮
        QPushButton *selectButton = new QPushButton("选择文件", centralWidget);
        selectButton->setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;");
        connect(selectButton, &QPushButton::clicked, this, &EncodingDetectorWindow::detectEncoding);
        mainLayout->addWidget(selectButton);

        // 结果文本框（可复制）
        resultField = new QTextEdit(centralWidget);
        resultField->setFixedHeight(120);
        resultField->setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;");
        resultField->setText("请选择一个文件以检测其编码");
        resultField->setReadOnly(false); // 允许复制
        mainLayout->addWidget(resultField);

        // 添加拉伸以保持布局整洁
        mainLayout->addStretch();

        // 设置窗口背景
        setStyleSheet("background-color: #f0f0f0;");
    }

private slots:
    void detectEncoding() {
        QString filePath = QFileDialog::getOpenFileName(
            this, "选择文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        );
        if (filePath.isEmpty()) {
            resultField->setText("未选择文件");
            return;
        }

        try {
            QFile file(filePath);
            if (!file.open(QIODevice::ReadOnly)) {
                resultField->setText("错误: 无法打开文件");
                return;
            }

            // 读取文件原始字节
            QByteArray rawData = file.readAll();
            file.close();

            QString encoding = "未知编码";
            QString resultText;

            // 检查 UTF-8-BOM
            const QByteArray bomUtf8 = QByteArray::fromRawData("\xEF\xBB\xBF", 3);
            if (rawData.startsWith(bomUtf8)) {
                encoding = "UTF-8-BOM";
                resultText = QString("文件: %1\n编码: %2\n置信度: 100%").arg(filePath, encoding);
                resultField->setText(resultText);
                return;
            }

            // 尝试以 UTF-8 读取
            QStringDecoder utf8Decoder(QStringDecoder::Utf8);
            QString utf8Text = utf8Decoder.decode(rawData);
            bool isUtf8Valid = !utf8Decoder.hasError();
            if (isUtf8Valid) {
                encoding = "UTF-8";
                resultText = QString("文件: %1\n编码: %2\n置信度: 90%").arg(filePath, encoding);
                resultField->setText(resultText);
                return;
            }

            // 尝试以 ASCII 读取
            bool isAscii = true;
            for (char c : rawData) {
                if (static_cast<unsigned char>(c) > 127) {
                    isAscii = false;
                    break;
                }
            }
            if (isAscii) {
                encoding = "ASCII";
                resultText = QString("文件: %1\n编码: %2\n置信度: 100%").arg(filePath, encoding);
                resultField->setText(resultText);
                return;
            }

            // 尝试以 CP1252 (ANSI) 读取
            QStringDecoder cp1252Decoder("Windows-1252");
            if (cp1252Decoder.isValid()) {
                QString cp1252Text = cp1252Decoder.decode(rawData);
                bool isCp1252Valid = !cp1252Decoder.hasError();
                if (isCp1252Valid) {
                    encoding = "ANSI (CP1252)";
                    resultText = QString("文件: %1\n编码: %2\n置信度: 80%").arg(filePath, encoding);
                    resultField->setText(resultText);
                    return;
                }
            }

            // 如果都失败，显示未知编码
            resultText = QString("文件: %1\n编码: %2\n置信度: 0%").arg(filePath, encoding);
            resultField->setText(resultText);

        } catch (const std::exception &e) {
            resultField->setText(QString("错误: %1").arg(e.what()));
        }
    }

private:
    QTextEdit *resultField;
};

#include "main.moc"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    EncodingDetectorWindow window;
    window.show();
    return app.exec();
}