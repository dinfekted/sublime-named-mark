<?php

// php is mainstream, isn't it? =)

class SomeClass {

  public function actionUpload() {
      $file = UploadedFile::getInstanceByName('file');

      // mark will be added here
      // cursor will come back after a while
      if($file == null || !preg_match('/^image|video/', $file->type)) {
          throw new HttpException(404);
      }

      $name = FileDrop::getUniqueContentName($file->getExtension());
      if($file->saveAs(FileDrop::getPath($name))) {
          return Json::encode([
              'name' => $name,
              'url' => FileDrop::getUrl($name, [108, 54]),
          ]);
      }
      // mark will be added here and everything to mark will be commented

      throw new HttpException(404);
  }

}