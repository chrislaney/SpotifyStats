# Hourly Contribution - Noah Falanga

## Fall Semester Summary
| Task                                                              | Hours        |
|-------------------------------------------------------------------|--------------|
| Research Flask backend integrations                               | 1            |
| Familiarize, analyze song features, capabilities from Spotify API | 4            |
| Select features, brainstorm data representation for learning      | 6            |
| Extra-meeting assignment work                                     | 8            |
| Meetings, extra-meeting communication                             | 12           |
| **Fall Semester Total**                                           | **31 hours** |

## Spring Semester Summary
| Task                                                                                                                    | Hours        |
|-------------------------------------------------------------------------------------------------------------------------|--------------|
| Pivot brain-storming (feature selection, clustering)                                                                    | 3            |
| Clustering algorithm script creation, selection, tuning [code](../spotifystats-code/main/cluster_tests/cluster_test.py) | 12           |
| Implementation of clustering upon creation in main [code](../spotifystats-code/main/main.py)                            | 2            |
| Creation of and implementation of clusterer wrapper [code](../spotifystats-code/main/clusterer.py)                      | 4            |
| Creation and tweaking of cluster gathering, playlist generation [code](../spotifystats-code/main/playlist_utils.py)     | 4            |
| Bug fixes and testing                                                                                                   | 8            |
| Extra-meeting assignment work                                                                                           | 10           |
| Meetings extra-meeting communication                                                                                    | 14           |
| **Spring Semester Total**                                                                                               | **55 hours** |

## Total Annual Contribution
**86 hours total for the academic year**

## Justifications of activities

The best way to justify my acitivities would simply be to walk through them one by one and explain the utility and duration of each activity.

Researching flask and how a backend would integrate into it was necessary as I was working on the backend of a flask application. 
It was incredibly short, as I already had experience in flask apps.
Familiarizing myself with the Spotify API was incredibly important, as it was the crutch that our project depended on; all our data came from Spotify, and thus
we needed to study it to make sure we gathered the correct data and features needed to fulfill our goals. It took four hours because the documentation was new to all of us,
and third party API's were also somewhat novel to me.
Selecting featurees and brainstorming data took place many times throughout discord and independently; I would reflect upon classwork 
I was taking currently or have taken in the past and thought about algorithms applicable with the data we had now. This took six hours because I was biting off
more than I could chew, and in each meeting we had to reflect on the practicality of the (in hindsight, foolish) scoring algorithms I was proposing.
Extra-meeting assignment work is fairly self-explanatory; we had quite a few assignments, and I spent an hour or two outside of meetings working on them. 
Meetings and extra-meeting communication is also in the same vein.

For the Spring, I produced much more practical, tangible work. With Spotify deprecating its API, namely its individual song features, we were given a 
blessing and curse in our much more limited scope of data to work with. We were able to figure out, then, that we could use genre information, and 
a clustering algorithm that groups users based on similar taste, which later became a focal point of our project. This took about three hours.
For the clustering algorithm, the script creation was important as it allowed us to test many different configurations of different clustering algorithms.
This was necessary because we wanted a good clustering of users with clusters that represented them without being too small. Justin's pre-existing functions
helped, but cleaning up my own and analyzing the results took a while, which is why the hefty 12 hours mark is present.
Implementing a clustering algorithm in main was fairly easy; I just needed to integrate it with our database to pull live users. It was necessary for labeling
users.
Implementation of the clusterer class was necessary as it provided a helpful and useful wrapper around the kmeans clustering class from sci-kit that
can be expanded in functionality later without changing the interface in which other functions operate with the object. This took about four hours.
The creation and tweaking of the cluster gathering and playlist generation was crucial, as it was important that clusters were identified based on distance, and that 
from those clusters a good representation of users' songs were picked such that the playlist reflects the given goal. This took four hours, with most of it 
being manual tweaking and analysis of generated playlists. 
Bug fixing and testing is pretty self-explanatory and was required and frequent when integrating isolated code into the connected system. 
The extra-meeting assignment work and meetings are also in the same vein as the previous semester, with more meeting time being included as we would
show our changes to each other in meetings.
