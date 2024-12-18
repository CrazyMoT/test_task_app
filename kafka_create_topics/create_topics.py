from confluent_kafka.admin import AdminClient, NewTopic

def create_topics(bootstrap_servers, topics):
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    existing_topics = admin_client.list_topics().topics.keys()

    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics if topic not in existing_topics]

    if new_topics:
        fs = admin_client.create_topics(new_topics)

        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print("All topics already exist")

if __name__ == "__main__":
    bootstrap_servers = 'kafka:9092'
    topics = ['transactions', 'notifications']
    create_topics(bootstrap_servers, topics)
