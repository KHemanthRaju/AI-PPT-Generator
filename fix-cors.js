// Quick CORS fix - test this URL directly in browser
const testAPI = async () => {
  try {
    const response = await fetch('https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        description: 'Test presentation',
        urls: [],
        slide_count: 3
      })
    });
    
    const data = await response.json();
    console.log('API Response:', data);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Run test
testAPI();