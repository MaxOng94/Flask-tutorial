from app import app_obj



# basically means if we run this python file directly, we will be in
# debug mode. THis means we can edit our codes, refresh our browser to see the effects of our changes
# this is as oppose to in production mode

if __name__ == "__main__":
    app_obj.run(debug =True)
