const fs = require('fs');

async function testPost() {
  const authRes = await fetch('https://bsky.social/xrpc/com.atproto.server.createSession', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier: 'mantralabs.web.id', password: 'nzom-geux-ssm2-gckc' })
  });
  const authData = await authRes.json();
  console.log('Login:', authData.handle, authData.did);

  const cleanTitle = 'Iran War Breathes New Life Into Turkmenistan Pipeline';
  const articleUrl = 'https://mantralabs.web.id/articles/iran-war-breathes-new-life-into-turkmenistans-10-billion-pipeline.html';
  const postText = `⚡ MANTRA LABS // WIRE DISPATCH\n\n📊 [COMMODITIES & ENERGY]\n${cleanTitle}\n\nEurasian transit corridors adjust to geopolitical embargoes.\n\n🔗 Read analysis:\n#Macro #Finance #Geopolitics`;

  const externalObj = {
    uri: articleUrl,
    title: cleanTitle.slice(0, 100),
    description: 'Institutional analysis on geopolitical energy transit corridors and Eurasian energy security.'
  };

  const record = {
    $type: 'app.bsky.feed.post',
    text: postText,
    createdAt: new Date().toISOString(),
    embed: {
      $type: 'app.bsky.embed.external',
      external: externalObj
    }
  };

  const resp = await fetch('https://bsky.social/xrpc/com.atproto.repo.createRecord', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + authData.accessJwt,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      repo: authData.did,
      collection: 'app.bsky.feed.post',
      record: record
    })
  });

  const res = await resp.json();
  console.log('Post status:', resp.status, res);
}

testPost();
