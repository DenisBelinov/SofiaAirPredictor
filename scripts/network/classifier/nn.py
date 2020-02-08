import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from random import shuffle

DATA_PATH = "/Users/belinovd/Personal/AI/SofiaAirPredictor/data/final/mladostFinal"
#DATA_PATH = "/Users/belinovd/Personal/AI/SofiaAirPredictor/data/final/ALL"
COLUMNS = {"temperature": 1, "windSpeed": 2, "humidity": 4, "precipIntensity": 5, "p1": 7}
UPPER_BOUNDS = {"green": 25, "yellow": 50, "orange": 75, "red": 100, "purple": 500}

FEATURES_COUNT = 4
CLASSES_COUNT = 5


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(FEATURES_COUNT, FEATURES_COUNT)

        self.fc2 = nn.Linear(FEATURES_COUNT, CLASSES_COUNT)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return F.log_softmax(x, dim=1)


def get_data():
    """
    1. Gets the data from DATA_PATH
    2. Cuts only columns from COLUMNS
    3. classifies p1 on ranges
    :return: TODO
    """
    trimmed_data = []
    with open(DATA_PATH, "r") as data_file:
        header = data_file.readline()

        unfiltered_data = data_file.readlines()
        data = []
        for line in unfiltered_data:
            if len(line.split()) < 9:
                # line is faulty
                continue
            data.append(line)

        trimmed_data = [[line.split()[i] for i in COLUMNS.values()] for line in data]

    result = []
    for entry in trimmed_data:
        features = entry[:-1]
        p1 = entry[-1]

        if float(p1) < UPPER_BOUNDS["green"]:
            cl = 0
        elif float(p1) < UPPER_BOUNDS["yellow"]:
            cl = 1
        elif float(p1) < UPPER_BOUNDS["orange"]:
            cl = 2
        elif float(p1) < UPPER_BOUNDS["red"]:
            cl = 3
        else:
            cl = 4

        result.append([features, cl])

    return result


if __name__ == "__main__":
    dataset = get_data()
    shuffle(dataset)

    dataset_size = len(dataset)
    testset = dataset[:int(dataset_size/5)]
    trainset = dataset[int(dataset_size/5):]

    net = Net()
    x = torch.tensor([0.1, 13.2, 0.3, 0.4])

    optimizer = optim.Adam(net.parameters(), lr=0.001)

    EPOCHS = 30
    BATCH_SIZE = 32

    for epoch in range(EPOCHS):
        shuffle(trainset)
        for i in range(0, len(trainset), BATCH_SIZE):
            batch = trainset[i:(i + BATCH_SIZE)]

            data = [list(map(float, b[0])) for b in batch]
            classes = [b[1] for b in batch]

            X = torch.tensor(data)
            y = torch.tensor(classes)
            output = net(X.view(-1, FEATURES_COUNT))

            loss = F.nll_loss(output, y)
            loss.backward()
            optimizer.step()

        print(loss)





    # TESTING NN
    shuffle(testset)

    TEST_BATCH_SIZE = 4
    correct = 0
    total = 0

    correct_guesses = {0:0, 1:0, 2:0, 3:0, 4:0}
    wrong_guesses = {0:0, 1:0, 2:0, 3:0, 4:0}

    with torch.no_grad():
        for i in range(0, len(testset), TEST_BATCH_SIZE):
            batch = testset[i:(i + TEST_BATCH_SIZE)]

            data = [list(map(float, b[0])) for b in batch]
            classes = [b[1] for b in batch]

            X = torch.tensor(data)
            y = torch.tensor(classes)

            output = net(X.view(-1, FEATURES_COUNT))
            for idx, i in enumerate(output):
                if torch.argmax(i) == y[idx]:
                    correct_guesses[int(y[idx])] += 1
                    correct += 1
                else:
                    wrong_guesses[int(y[idx])] += 1
                total += 1

    print('Accuracy of the network: %d %%' % (
            100 * correct / total))
    print("correct guesses:", correct_guesses)
    print("wrong_guesses:", wrong_guesses)

    # this is used for data analysis if needed
    # counts = {"green": 0, "yellow": 0, "orange": 0, "red": 0, "purple": 0}
    #
    # for data in dataset:
    #     counts[data[1]] += 1
    #
    # print(counts)

