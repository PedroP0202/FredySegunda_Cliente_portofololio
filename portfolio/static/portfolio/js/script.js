function triggerUpload(id){
  if (document.body.classList.contains('admin-mode')) {
    document.getElementById(id).click();
  }
}

function loadMedia(input, placeholderId, lbId){
  const file = input.files[0];
  if(!file) return;
  const url = URL.createObjectURL(file);
  const ph = document.getElementById(placeholderId);
  const isVideo = file.type.startsWith('video/');
  const slot = ph ? ph.closest('.media-slot, .reel-item') : null;

  if(ph){
    if(isVideo){
      const v = document.createElement('video');
      v.src = url;
      v.autoplay = true;
      v.muted = true;
      v.loop = true;
      v.playsInline = true;
      v.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;';
      ph.replaceWith(v);
    } else {
      const img = document.createElement('img');
      img.src = url;
      img.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;';
      ph.replaceWith(img);
    }
  }

  if(slot){
    slot.dataset.mediaUrl = url;
    slot.dataset.mediaType = isVideo ? 'video' : 'image';
    slot.addEventListener('click', function(e){
      if(e.target.tagName === 'INPUT') return;
      openLightbox(this.dataset.mediaUrl, this.dataset.mediaType);
    }, {once: false});
  }
}

function openLightbox(url, type){
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const vid = document.getElementById('lb-vid');
  if(type === 'video'){
    vid.src = url;
    vid.style.display = 'block';
    img.style.display = 'none';
  } else {
    img.src = url;
    img.style.display = 'block';
    vid.style.display = 'none';
    vid.src = '';
  }
  lb.classList.add('open');
}

function closeLightbox(e){
  if(e.target.id === 'lightbox'){
    document.getElementById('lightbox').classList.remove('open');
    document.getElementById('lb-vid').pause();
  }
}

document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){
    document.getElementById('lightbox').classList.remove('open');
    document.getElementById('lb-vid').pause();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');
  if (logo) {
    logo.addEventListener('dblclick', () => {
      const pwd = prompt("Password para modo edição:");
      if (pwd === "admin123") {
        document.body.classList.add('admin-mode');
        alert("Modo de edição ativado!");
      }
    });
  }
});
