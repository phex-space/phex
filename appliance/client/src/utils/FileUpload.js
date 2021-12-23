export class FileUpload {
  constructor(name, files) {
    this.name = name;
    this.files = files;
    this.uploadedSize = 0;
    this.totalSize = Array.from(files).reduce(
      (previous, current) => previous + current.size,
      0
    );
    this.headers = {};
  }

  setHeader = (name, value) => {
    if (value != null) this.headers[name] = value;
    else delete this.headers[name];
  };

  send = (url) => {
    return new Promise((resolve, reject) => {
      Promise.all(
        Array.from(this.files).map((file) => {
          return this.doSend(url, file);
        })
      )
        .then((responses) => {
          resolve(responses);
        })
        .catch((errors) => reject(errors));
    });
  };

  doSend = (url, file) => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const fd = new FormData();
      let rejected = false;

      xhr.open("POST", url, true);
      Object.keys(this.headers).forEach((header) => {
        xhr.setRequestHeader(header, this.headers[header]);
      });
      xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && !rejected) {
          resolve(xhr);
        }
      };
      xhr.addEventListener("load", (ev) => {});
      xhr.addEventListener("error", (ev) => {
        rejected = true;
        reject(xhr);
      });
      xhr.upload.addEventListener("progress", (ev) => {
        if (ev.lengthComputable) {
          this.uploadedSize += ev.loaded;
        }
      });
      fd.append(this.name, file);
      xhr.send(fd);
    });
  };
}
