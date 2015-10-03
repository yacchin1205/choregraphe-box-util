# How to install

以下のpipコマンドで依存関係含めインストールできます。

```
$ pip install git+https://github.com/yacchin1205/choregraphe-box-util.git
```

# How to use

## replace-boxes

ボックスの置き換えをおこなうためのコマンドです。

あるプロジェクトに関して、指定したボックスライブラリのボックスが使用されている場合に、ビヘイビア中のボックスを最新のものへと
置き換えることができます。

```
$ replace-boxes --lib (ボックスライブラリのパス: ディレクトリのみ可) (プロジェクトの.pmlファイルへのパス)
```

このように実行すると、プロジェクトのうちボックスライブラリ中のボックスを使用している個所は自動的に置き換えられます。

なお、ボックスの説明には以下のように、 `@source` という記述により、ボックスがどこで配布されているかを識別するURLを記述されている必要があります。

```
Subscribes to an event in ALMemory.
When an event is raised, the output is fired.

The box is implemented using qi Framework.

ALMemory中のイベントを監視します。監視対象のイベントが発火すると、onEvent出力が発火します。

このボックスはqi Frameworkを利用して実装されています。


@source https://github.com/yacchin1205/pepper-web-boxes
```

このようにすることで、同名だが異なる場所から取得したボックスを誤って置き換えることを防止することができます。(`--ignore-tags` オプションによりこの動作を抑制できます。)

他に使用可能なオプションについては、`-h` オプションでヘルプを参照することができます。

```
$ replace-boxes -h
```
