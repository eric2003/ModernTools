#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QRegularExpression>

class PathConverter : public QWidget {
    Q_OBJECT

public:
    PathConverter(QWidget *parent = nullptr) : QWidget(parent) {
        auto *layout = new QVBoxLayout(this);

        inputEdit = new QLineEdit(this);
        inputEdit->setPlaceholderText("请输入路径");
        layout->addWidget(inputEdit);

        convertButton = new QPushButton("转换路径", this);
        connect(convertButton, &QPushButton::clicked, this, &PathConverter::onConvertClicked);
        layout->addWidget(convertButton);

        outputLabel = new QLabel(this);
        outputLabel->setWordWrap(true);
        layout->addWidget(outputLabel);
    }

private slots:
    void onConvertClicked() {
        QString path = inputEdit->text();
        QRegularExpression re("\\\\");
        QRegularExpressionMatchIterator it = re.globalMatch(path);
        QString convertedPath = it.hasNext() ? path.replace(re, "/") : path;
        outputLabel->setText(convertedPath);
    }

private:
    QLineEdit *inputEdit;
    QPushButton *convertButton;
    QLabel *outputLabel;
};

#include "main.moc"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    PathConverter window;
    window.show();

    return app.exec();
}