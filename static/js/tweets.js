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
}

function getParameterByName(name, url=window.location.href) {
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function attachTweet(tweetValue, prepend=false, retweet){
  const currentUser = document.getElementById("current-user").getAttribute('data-user');
  let tweetHTML;
  if (retweet && tweetValue.parent) {
    const mainTweet = tweetValue.parent;
    tweetHTML = `
      <small style="color:#ccc;">Retweeted Via ${tweetValue.user.username} at ${tweetValue.timesince}</small>
      <h5 class="mt-0 tweet-content">${tweetValue.content}</h5>
      <p>via <a href="${mainTweet.user.url}">${mainTweet.user.username}</a> | ${ mainTweet.timesince }
        <a href="${mainTweet.url}">view</a>
        | <a class="retweet" id="${tweetValue.parent.id}" href="${tweetValue.parent.retweet_url}">Retweet</a>
        | <a class="like" href="${tweetValue.parent.like_url}">Like</a>
        `;
  } else {
    tweetHTML = `
      <h5 class="mt-0 tweet-content" >${tweetValue.content}</h5>
      <p>via <a href="${tweetValue.user.url}">${tweetValue.user.username}</a> | ${ tweetValue.timesince }
        <a href="${tweetValue.url}">view</a>
        | <a class="retweet" id="${tweetValue.id}" href="${tweetValue.retweet_url}">Retweet</a>
        | <a class="like" href="${tweetValue.like_url}">Like</a>
        `;
  }
  if (currentUser == tweetValue.user.username) {
    tweetHTML +=
      `
      | <a href="${tweetValue.update_url}">update</a> |
      <a href="${tweetValue.delete_url}">delete</a>
      </p>
      <hr>
    `
  } else {
    tweetHTML += `
      </p>
      <hr>
    `
  };
  if (prepend) {
    div.insertAdjacentHTML('afterbegin', tweetHTML);
  } else {
    div.innerHTML += tweetHTML;
  }
}
  
  
function retweet() {
  document.addEventListener("DOMContentLoaded", function() {
    document.body.addEventListener("click", function(e) {
      if (e.target.classList.contains("retweet")) {
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
  });
}

function updateHashLinks(){
  const hashtagRegex = /(^|\s)#([\w\d]+)/g;
  const usernameRegex = /(^|\s)@([\w\d]+)/g;
  const tweets = div.querySelectorAll('.tweet-content');
  tweets.forEach((value) => {
    value.innerHTML = value.innerHTML.replace(hashtagRegex, `$1<a href='/hashtag/$2/'>#$2</a>`).replace(usernameRegex, ` $1<a href='/account/$2/'>@$2</a>`);
  });
}



function fetchTweets(url) {
  // let fetchUrl;
  // if (!url) {
  //   fetchUrl = getParameterByName('q') ? "/api/tweet/?q=" + getParameterByName('q') : '/api/tweet/';
  // } else {
  //   fetchUrl = getParameterByName('q') ? url + getParameterByName('q') : url;
  // }
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
  div.addEventListener('click', (e) => {
    e.preventDefault();
    // const this_ = e.target;
    if (e.target.classList.contains('like')) {
      const likeURL = e.target.href; 
      fetch(likeURL, {
        method: 'GET',
      })
      .then(response => response.json())
      .then(data => {
        if (data && data.liked) {
          e.target.textContent = 'Liked';
          // attachTweet(data, prepend=true, retweet=true);
          // updateHashLinks();
        } else {
          e.target.textContent = 'Unliked';
          // alert(data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    }
  });
}


