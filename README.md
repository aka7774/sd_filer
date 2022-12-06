# sd_filer
File Management of Models, Hypernetworks, Extensions, and Images.

- Filer(フィレール)は、フランス語で「紡ぐ」という意味です
  - ただのファイラーです
- ハードディスクとファイルをやりとりするのに便利
  - クラウドでも便利かと思ったけどたぶん備え付けのツールのほうが便利

# At your own risk

- Deleteボタンを押すと選択したファイルが消えます
- その他何があっても作者は責任を負いません

## UI機能は打ち止め

- gradioでUIを作りこむのは非常に困難だとわかったのでUIはこれ以上凝らない

# Backup Directory

- 保存先のディレクトリをフルパスで入力してください
- 近い将来ここは親ディレクトリを指定する仕様に変更する
  - タブごとにサブフォルダ作って保存する予定

# 共通

## Reload

- 最初にReloadを押さないと動きません
- 最初から読み込むと1111の起動に時間がかかるのでどうしたものか
  - タブ押したときに読み込むのは難しそう

## Save (genre) comment

- 自動保存に出来るけど破損の可能性もありうるのでボタンにした
- Active / Backup を問わず、ファイル名に対してコメントがつきます
  - 移動してもコメントは有効

## Copy / Move

- shutil の copy() と move()
- 進捗表示出せるかは未調査だけど期待してない

## Delete

- os.remove()

# Checkpoint

- 拡張子ckptとsafetensorに対応

## Make InvokeAI models.yaml

- https://github.com/aka7774/sd_invokeai_models_yaml_maker
- InvokeAI/configs/models.yaml の中身を生成する
- 選択したモデルだけ出力できる
- Backupにあるものも指定できる

## Calc SHA256

- ファイルのSHA256フルハッシュを計算する
- ファイル名.sha256 ファイルに保存する(二重拡張子になる)
- 頭8桁だけを一覧に表示するが滅多に重複しないはず(するようなら桁を増やす)

## vae.pt

- 同名の.vae.ptファイルが存在すれば Y を表示

## yaml

- 同名の.yamlファイルが存在すれば Y を表示

## Genre

- モデルがどういう風に作られたかのメモ(任意)

## Comment

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
