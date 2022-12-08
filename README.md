# sd_filer
File Management of Models, Hypernetworks, Extensions, and Images.

- Filer(フィレール)は、フランス語で「紡ぐ」という意味です
  - ただのファイラーです
- ハードディスクとファイルをやりとりするのに便利
  - クラウドでも便利かと思ったけどたぶん備え付けのツールのほうが便利

# At your own risk

- Deleteボタンを押すと選択したファイルが消えます
- 複数のブラウザタブ等を開いて異なる設定で動作させることはできません
- その他何があっても作者は責任を負いません

## UI機能は打ち止め

- gradioでUIを作りこむのは非常に困難だとわかったのでUIはこれ以上凝らない

# 共通

## Backup Directory

- 保存先のディレクトリをフルパスで入力してください
- 近い将来ここは親ディレクトリを指定する仕様に変更する
  - タブごとにサブフォルダ作って保存する予定

## Extension内のjsonフォルダ

- Backup Directoryの場所が保存されます
- genre/commentが保存されます

## Activeタブ

- 1111が認識しているファイルが表示されます

## Backupタブ

- Backup Directory内のファイルが表示されます

## Reloadボタン

- 最初にReloadを押さないと動きません
- 最初から読み込むと1111の起動に時間がかかるのでどうしたものか
  - タブ押したときに読み込むのは難しそう

## Save commentsボタン

- comment, genre, modelなど記入した内容を保存する
- 自動保存に出来るけど破損の可能性もありうるのでボタンにした
- Active / Backup を問わず、ファイル名に対してコメントがつきます
  - 移動してもコメントは有効

## Downloadボタン

- 選択したファイルをダウンロードできる一覧を画面下部に表示します
- ファイルの場合
  - このボタンを押した時点でtmpにファイルがコピーされます
- ディレクトリの場合
  - このボタンを押した時点でtmpにzipが作成されます
- 画面下部のdownloadリンクを押すとダウンロード開始

## Copy / Moveボタン

- Copy
  - ファイルは shutil.copy()
  - ディレクトリは shutil.rmtree()
- Move
  - どちらも shutil.move()
- 進捗表示出せるかは未調査だけど期待してない

## Deleteボタン

- ファイルは os.remove()
- ディレクトリは shutil.rmtree()

# Checkpoint

- 拡張子ckptとsafetensorに対応

## Make InvokeAI models.yamlボタン

- https://github.com/aka7774/sd_invokeai_models_yaml_maker
- InvokeAI/configs/models.yaml の中身を生成する
- 選択したモデルだけ出力できる
- Backupにあるものも指定できる

## Calc SHA256ボタン

- ファイルのSHA256フルハッシュを計算する
- ファイル名.sha256 ファイルに保存する(二重拡張子になる)
- 頭8桁だけを一覧に表示するが滅多に重複しないはず(するようなら桁を増やす)

## vae.pt列

- 同名の.vae.ptファイルが存在すれば Y を表示

## yaml列

- 同名の.yamlファイルが存在すれば Y を表示

## Genre列

- モデルがどういう風に作られたかのメモ(任意)

## Comment列

- メモ(任意)

## 解説

- 実装はCheckpoint Managerを参考にした
  - https://github.com/rvhfxb/checkpoint_manager
- 1111の「Stable Diffusion checkpoint」ドロップダウンをいじる方法は現状存在しなさそう
  - BackupにMoveすれば当然リストからは消える
- X/Y Plotの「Checkpoint」にはファイル名が有効で、「Selected」をコピペして使える
  - 拡張子無しで動くが、safetensor対応に伴って拡張子はつけることにした
- Copy/Move/Deleteに.vae.ptと.yamlを追随させる機能を検討したい気持ちはある
  - チェックボックスでオンオフとか
  - でもvaeは数が少ないしyamlは容量が小さいのでほっといてもいいかなー

# Hypernetworks

## state列

- state_dictにファイルの詳細情報が格納されているのでそれを表示する
- torch.load()しないといけなくて複数ファイルだと結構時間がかかる
- エラーが出るファイルがあるけど原因は深追いしていない

## model列

- どのモデル用のファイルとして作ったかのメモを想定

## 解説

- ファイルのStepsを保存する統一仕様は存在していなさそう
- ファイル名につけている事もある(state_dictのnameは一緒)
- ファイル名が一緒でstate_dictに入っているnameを変えてる事もある
- state_dictにnameが入っていないケースも想定されている
- 元のモデル情報が入っていることもあるらしいが見つかっていない
- 学習ファイルについては、当面は自己管理を徹底するしか無さそう

# Extensions

- ファイルは表示対象外
- 自分自身(sd_filer Extension)も表示対象外

## Move / Delete

Windows だとダメかも

- PermissionError: [WinError 5] で一部ファイル(.git内のオブジェクト)のアクセスが拒否される
- ディレクトリの内容は中途半端になる
- sd_filer が copy したファイルでもダメ
- かといって管理者権限でgradioを実行しましょうと言う気もないので諦める

# Images

- ディレクトリ単位
- ファイル単位の処理には Image Browser を使いましょう

## 一覧に表示されるディレクトリ

- 既定の6つ
  - opts.outdir_txt2img_samples
  - opts.outdir_img2img_samples
  - opts.outdir_extras_samples
  - opts.outdir_txt2img_grids
  - opts.outdir_img2img_grids
  - opts.outdir_save
- generate_from_jsonの2つ(インストールディレクトリを変更していない場合のみ)
  - json
  - webp
- Image Browser の Others タブで追加したディレクトリ
  - path_recorder.txtに保存されている

## Move / Delete

- ディレクトリ内の全ファイルではなくディレクトリごと処理します
- よって元のディレクトリは無くなります
