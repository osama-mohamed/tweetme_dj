let div;
const loadMore = document.getElementById('load-more');
let nextTweetUrl;
let tweetList;

function divID(id, create=false, url='') {
  div = id ? document.getElementById(id) : document.getElementById('tweet-container');
  url ? fetchTweets(url) : fetchTweets();
  if (create) {
    tweetFormPreSubmit();
  }
  retweet();
  tweetLike();
  reply();
}

function getParameterByName(name, url=window.location.href) {
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
  results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function formatTweet(tweetValue) {
  let isReply = tweetValue.reply;
  const currentUser = document.getElementById("current-user").getAttribute('data-user');
  let preContent;
  if (tweetValue.parent && !isReply) {
    tweetValue = tweetValue.parent;
    preContent = `<small style="color:#ccc;">Retweeted Via ${tweetValue.user.username} at ${tweetValue.timesince}</small>`;
  } else if (tweetValue.parent && isReply) {
    isReply = true;
    preContent = `<small style="color:#ccc;">Replying to @${tweetValue.parent.user.username} at ${tweetValue.parent.timesince}</small>`;
  }
  let verb = 'Like';
  if (tweetValue.did_like) {
    verb = 'Unlike';
  }
  let tweetContent = `
  <h5 class="mt-0" >${tweetValue.content}</h5>
  <p>via <a href="${tweetValue.user.url}">${tweetValue.user.username}</a> | ${ tweetValue.timesince }
    <a href="${tweetValue.url}">view</a>
    | <a class="retweet" id="${tweetValue.id}" href="${tweetValue.retweet_url}">Retweet</a>
    | <a class="like" href="${tweetValue.like_url}">${verb} (${tweetValue.likes})</a>
    | <a class="reply" id="${tweetValue.id}" data-user="${tweetValue.user.username}" href="#">Reply</a>
  `;
  if (currentUser == tweetValue.user.username) {
    tweetContent +=
      `
      | <a href="${tweetValue.update_url}">update</a> |
      <a href="${tweetValue.delete_url}">delete</a>
      </p>
    `
  } else {
    tweetContent += `
      </p>
    `
  };
  let container;
  if (preContent) {
    container = `<div class="tweet-container">${preContent}${tweetContent}<hr></div>`;
  } else {
    container = `<div class="tweet-container">${tweetContent}<hr></div>`;
  }
  return container;
}


function attachTweet(tweetValue, prepend=false, retweet){
  const tweetHTML = formatTweet(tweetValue);
  if (prepend) {
    div.insertAdjacentHTML('afterbegin', tweetHTML);
  } else {
    div.innerHTML += tweetHTML;
  }
}


function retweet() {
  div.addEventListener("click", function(e) {
    if (e.target.matches(".retweet")) {
      e.preventDefault();
      const tweetId = e.target.id;         
      const retweetURL = window.location.origin + '/api/tweet/' + tweetId + '/retweet/';
      fetch(retweetURL, {
        method: 'GET',
      })
      .then(response => response.json())
      .then(data => {
        if (data && data.url) {
          attachTweet(data, prepend=true, retweet=true);
          updateHashLinks();
        } else {
          alert(data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    }
  });
}

function updateHashLinks(){
  const hashtagRegex = /(^|\s)#([\w\d]+)/g;
  const usernameRegex = /(^|\s)@([\w\d]+)/g;
  // const tweets = div.querySelectorAll('.tweet-content');
  // tweets.forEach((value) => {
  //   value.innerHTML = value.innerHTML.replace(hashtagRegex, `$1<a href='/hashtag/$2/'>#$2</a>`).replace(usernameRegex, ` $1<a href='/account/$2/'>@$2</a>`);
  // });
  const tweets = document.querySelectorAll('.tweet-container');
  tweets.forEach((tweet) => {
    const elementsToCheck = tweet.querySelectorAll('small, h5, p, a');
    elementsToCheck.forEach((element) => {
      if (element instanceof HTMLElement) {
        element.innerHTML = element.innerHTML.replace(hashtagRegex, `$1<a href='/hashtag/$2/'>#$2</a>`).replace(usernameRegex, ` $1<a href='/account/$2/'>@$2</a>`);
      }
    });
  });

}



function fetchTweets(url) {
  const fetchUrl = getParameterByName('q') ? url + getParameterByName('q') : url;
  fetch(fetchUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    tweetList = data.results;
    if (data.next){
      loadMore.style.display = 'block';
      nextTweetUrl = data.next;
    } else {
      loadMore.style.display = 'none';
    }
    if (tweetList == 0) {
      div.textContent = "No tweets currently found.";
    } else {
      data.results.forEach((value, key) => {
        if (value.parent){
          attachTweet(value, prepend=false, retweet=true);
        } else {
          attachTweet(value, prepend=false, retweet=false);
        }
        updateHashLinks();
      });
    }
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
}

loadMore.addEventListener('click', function(event) {
  event.preventDefault();
  if (nextTweetUrl) {
    fetchTweets(nextTweetUrl);
  }
});

const tweetform = document.getElementById('tweet-form');
function tweetFormPreSubmit() {
  const charsStart = 140;
  let charsCurrent = 0;
  tweetform.innerHTML += `<span id='tweetCharsLeft'>${charsStart}</span>`;
  document.getElementById('id_content').addEventListener('keyup', function(event) {
    let tweetContent = event.target.value;
    charsCurrent = charsStart - tweetContent.length;
    const spanChars = document.getElementById('tweetCharsLeft')
    spanChars.textContent = charsCurrent;
    if (charsCurrent > 0) {
      spanChars.classList.remove("grey-color");
      spanChars.classList.remove("red-color");
    } else if (charsCurrent === 0) {
      spanChars.classList.remove("red-color");
      spanChars.classList.add("grey-color");
    } else if (charsCurrent < 0) {
      spanChars.classList.remove("grey-color");
      spanChars.classList.add("red-color");
    }
  });

  tweetform.addEventListener('submit', function(event) {
    event.preventDefault();
    if (charsCurrent >= 0 ) {
      submitTweet(event);
    } else {
      alert('Your tweet is too long.');
    }
  });
}


function submitTweet(event){
  const formData = new FormData(event.target);
  const content = formData.get('content');
  let serializedData = {};
  for (const [key, value] of formData.entries()) {
    serializedData[key] = value;
  }
  const createURL = window.location.origin + tweetform.getAttribute('data-url');
  fetch(createURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': serializedData['csrfmiddlewaretoken'],
    },
    body: JSON.stringify(serializedData),
  })
  .then(response => response.json())
  .then(data => {
    event.target.reset();
    attachTweet(data, prepend=true, retweet=false);
    updateHashLinks();
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


function tweetLike() {
  div.addEventListener('click', function(e) {
    if (e.target.matches('.like')) {
      e.preventDefault();
      const likeURL = e.target.href; 
      fetch(likeURL, {
        method: 'GET',
      })
      .then(response => response.json())
      .then(data => {
        if (data && data.liked) {
          e.target.textContent = `Unlike (${data.likes})`;
        } else {
          e.target.textContent = `Like (${data.likes})`;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    }
  });
}


function reply() {
  div.addEventListener('click', function(e) {
    if (e.target.matches('.reply')) {
      e.preventDefault();
      const tweetId = e.target.id;
      const tweetUser = e.target.getAttribute('data-user');
      const myModal = new bootstrap.Modal(document.getElementById('replyModal'));
      let tweetContent = document.getElementById('tweetReplyArea');
      tweetContent.value = `@${tweetUser} `;
      myModal.show();
      myModal._element.addEventListener('shown.bs.modal', function () {
        tweetContent.focus();
        let hiddenInput = document.getElementById('hiddenInputId');
        hiddenInput.value = tweetId;
      });
      const tweetForm = document.querySelector('.tweet-form');
      tweetForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const content = tweetContent.value;        
        const replyURL = window.location.origin + tweetContent.getAttribute('data-url');
        const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value');
        tweetForm.reset();
        myModal.hide();
        fetch(replyURL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
          },
          body: JSON.stringify({
            'content': content,
            'parent_id': tweetId,
            'reply': true,
          }),
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          attachTweet(data, prepend = true, retweet = false);
          updateHashLinks();
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    }
  });
}

