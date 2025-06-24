#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QPushButton>
#include <QTextEdit>
#include <QFileDialog>
#include <QLabel>
#include <QString>
#include <QFile>
#include <QDirIterator>
#include <QStringConverter>
#include <QMap>
#include <QList>

class DirectoryEncodingDetectorWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit DirectoryEncodingDetectorWindow(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("目录文件编码检测器");
        setFixedSize(600, 500);

        // 创建主窗口部件和布局
        QWidget *centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);
        QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

        // 标题标签
        QLabel *titleLabel = new QLabel("目录文件编码检测器", centralWidget);
        titleLabel->setStyleSheet("font-size: 14pt; font-family: Arial; font-weight: bold;");
        titleLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(titleLabel);

        // 选择目录按钮
        QPushButton *selectButton = new QPushButton("选择目录", centralWidget);
        selectButton->setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;");
        connect(selectButton, &QPushButton::clicked, this, &DirectoryEncodingDetectorWindow::detectDirectoryEncoding);
        mainLayout->addWidget(selectButton);

        // 编码统计文本框（可复制）
        statsField = new QTextEdit(centralWidget);
        statsField->setFixedHeight(150);
        statsField->setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;");
        statsField->setText("请选择一个目录以检测其文件编码");
        statsField->setReadOnly(false); // 允许复制
        mainLayout->addWidget(statsField);

        // 非主流编码文件标签
        QLabel *minorityLabel = new QLabel("非主流编码文件：", centralWidget);
        minorityLabel->setStyleSheet("font-size: 12pt; font-family: Arial;");
        mainLayout->addWidget(minorityLabel);

        // 非主流编码文件列表文本框（可复制）
        minorityField = new QTextEdit(centralWidget);
        minorityField->setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;");
        minorityField->setText("非主流编码文件将显示在这里");
        minorityField->setReadOnly(false); // 允许复制
        mainLayout->addWidget(minorityField);

        // 设置窗口背景
        setStyleSheet("background-color: #f0f0f0;");
    }

private slots:
    void detectDirectoryEncoding() {
        QString directory = QFileDialog::getExistingDirectory(this, "选择目录");
        if (directory.isEmpty()) {
            statsField->setText("未选择目录");
            minorityField->setText("未选择目录");
            return;
        }

        try {
            // 收集所有文件的编码
            QMap<QString, int> encodingCounts;
            int totalFiles = 0;
            QList<QPair<QString, QString>> fileList;

            // 递归遍历目录
            QDirIterator it(directory, QDir::Files, QDirIterator::Subdirectories);
            while (it.hasNext()) {
                QString filePath = it.next();
                QFile file(filePath);
                if (!file.open(QIODevice::ReadOnly)) {
                    encodingCounts["错误"]++;
                    totalFiles++;
                    fileList.append({filePath, "错误"});
                    continue;
                }

                // 读取文件原始字节
                QByteArray rawData = file.readAll();
                file.close();
                if (rawData.isEmpty()) {
                    continue; // 跳过空文件
                }

                QString encoding = "未知编码";

                // 检查 UTF-8-BOM
                const QByteArray bomUtf8 = QByteArray::fromRawData("\xEF\xBB\xBF", 3);
                if (rawData.startsWith(bomUtf8)) {
                    encoding = "UTF-8-BOM";
                    encodingCounts[encoding]++;
                    totalFiles++;
                    fileList.append({filePath, encoding});
                    continue;
                }

                // 尝试以 UTF-8 读取
                QStringDecoder utf8Decoder(QStringDecoder::Utf8);
                QString utf8Text = utf8Decoder.decode(rawData);
                if (!utf8Decoder.hasError()) {
                    encoding = "UTF-8";
                    encodingCounts[encoding]++;
                    totalFiles++;
                    fileList.append({filePath, encoding});
                    continue;
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
                    encodingCounts[encoding]++;
                    totalFiles++;
                    fileList.append({filePath, encoding});
                    continue;
                }

                // 尝试以 CP1252 (ANSI) 读取
                QStringDecoder cp1252Decoder("Windows-1252");
                if (cp1252Decoder.isValid()) {
                    QString cp1252Text = cp1252Decoder.decode(rawData);
                    if (!cp1252Decoder.hasError()) {
                        encoding = "ANSI (CP1252)";
                        encodingCounts[encoding]++;
                        totalFiles++;
                        fileList.append({filePath, encoding});
                        continue;
                    }
                }

                // 未知编码
                encodingCounts[encoding]++;
                totalFiles++;
                fileList.append({filePath, encoding});
            }

            if (totalFiles == 0) {
                statsField->setText("目录中没有文件");
                minorityField->setText("无非主流编码文件");
                return;
            }

            // 确定主流编码（出现次数最多的编码）
            QString mostCommonEncoding;
            int maxCount = 0;
            for (auto it = encodingCounts.constBegin(); it != encodingCounts.constEnd(); ++it) {
                if (it.value() > maxCount) {
                    mostCommonEncoding = it.key();
                    maxCount = it.value();
                }
            }

            // 生成统计结果
            QString statsText = QString("目录: %1\n总文件数: %2\n\n编码统计:\n").arg(directory).arg(totalFiles);
            for (auto it = encodingCounts.constBegin(); it != encodingCounts.constEnd(); ++it) {
                double percentage = (it.value() * 100.0) / totalFiles;
                statsText += QString("%1: %2 个文件 (%3%)\n").arg(it.key()).arg(it.value()).arg(percentage, 0, 'f', 2);
            }

            // 找出非主流编码文件
            QStringList minorityFiles;
            for (const auto &file : fileList) {
                if (file.second != mostCommonEncoding && file.second != "错误") {
                    minorityFiles.append(QString("%1 (%2)").arg(file.first, file.second));
                }
            }
            QString minorityText = minorityFiles.isEmpty() ? "无非主流编码文件" : minorityFiles.join("\n");

            // 显示结果
            statsField->setText(statsText.trimmed());
            minorityField->setText(minorityText);

        } catch (const std::exception &e) {
            statsField->setText(QString("错误: %1").arg(e.what()));
            minorityField->setText("错误发生，无法列出非主流编码文件");
        }
    }

private:
    QTextEdit *statsField;
    QTextEdit *minorityField;
};

#include "main.moc"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    DirectoryEncodingDetectorWindow window;
    window.show();
    return app.exec();
}