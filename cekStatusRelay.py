from firebase import firebase
firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)
result = firebase.get('/sensor/relay', 'status')
print result
