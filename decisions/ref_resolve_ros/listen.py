#!/usr/bin/env python
import rospy
import reference_resolution
#from textblob import TextBlob as tb
#from textblob_aptagger import PerceptronTagger
from std_msgs.msg import String
import nltk.tag
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()
#ap_tagger = PerceptronTagger()


def talker():
    pub = rospy.Publisher('utterances', String, queue_size=10)
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        utterance_str = raw_input("Which object are you referring to? \n")    
        AR_referred_to = reference_resolution.resolve_reference(utterance_str, tagger)
        rospy.loginfo("AR code is: " + str(AR_referred_to))
        pub.publish(AR_referred_to)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
